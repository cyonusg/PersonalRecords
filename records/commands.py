import click
from datetime import date
from records.services import RecordService
from records.models import Record

@click.group()
def records():
    """ Manages the records lifecycle"""
    pass

@records.command()

def create():
    recordsMovement = _get_movements()
    click.echo(click.style('Select from the list the movement you want add new PR', fg='yellow', bold=True))

    _print_movements(recordsMovement)

    movement_id = click.prompt('Enter movement id eg. [pc] for Power Clean', type=str).upper().strip()

    movement_selected = list(filter(lambda movement: movement['id'] == movement_id, recordsMovement))
    
    record = click.prompt('Enter your {name} [{id}] PR'.format(
        name = movement_selected[0]['name'],
        id = movement_selected[0]['id']
    ), type=str)

    repetitions = click.prompt('Enter number of repetitions (1)', type=int,default=1)

    for movement in recordsMovement:
        if movement['id'] == movement_id:
            movement['records'].append({
                "date": str(date.today()),
                "weigth": record,
                "repetitions": repetitions,
            })
            break
            
    _update_file(recordsMovement)
    click.echo(click.style("record saved successfully", bg="green", fg="white", bold=True ))
    pass

@records.command()
def lists():
    """List all last record per movement"""
    recordsMovement = _get_movements()

    click.echo(click.style('ID | MOVEMENT | WEIGTH | DATE | REPETITIONS', fg='yellow', bold=True))
    click.echo(click.style('*' * 100, fg='green'))
    for movement in recordsMovement:
        if len(movement['records']) > 0:
            last_record = movement['records'][-1]
            click.echo('{id} | {movement} | {weigth} | {date} | {repetitions}'.format(
                                                                    id=movement['id'],
                                                                    movement=movement['name'],
                                                                    weigth=last_record['weigth'],
                                                                    repetitions=last_record['repetitions'],
                                                                    type=movement['type'],
                                                                    date=last_record['date']))
            click.echo(click.style('-' * 50, fg='green'))
    pass

@records.command()
@click.argument('movement_id', type=str)
@click.option('-h', '--historial', is_flag=True, default=None)

def get (movement_id, historial=None):
    """List last record for a movement"""
    recordsMovement = _get_movements()
    movement = _get_movement(recordsMovement, movement_id)
    
    if movement == None:
        click.echo(click.style('Insert valid movement', bg='red', fg='white', bold=True))
        return 

    if len(movement['records']) == 0:
        click.echo(click.style('{movement_name} not have record register', bg='red', fg='white', bold=True))
        return
    pass

    if historial :
        _get_record_history_movement(movement)
    else:
        _get_record_percentages_movement(movement)

@records.command()
@click.argument('movement_id', type=str)

def update (movement_id):
    recordsMovement = _get_movements()
    movement = _get_movement(recordsMovement, movement_id)
    
    if movement == None:
        click.echo(click.style('Insert valid movement', bg='red', fg='white', bold=True))
        return
    
    _get_record_history_movement(movement)
    
    record_id = click.prompt('Insert Number of Record you want to update', type=int, default=None)
    current_record_item = record_id -1
    movement['records'][current_record_item]['weigth'] = click.prompt('Insert new weigth', type=int, default=movement['records'][current_record_item]['weigth'])
    movement['records'][current_record_item]['repetitions'] = click.prompt('Insert new repetitions', type=int, default=movement['records'][current_record_item]['repetitions'])

    for movement_item in recordsMovement:
        if movement_item['id'] == movement_id:
            movement_item['records'][current_record_item] =  movement['records'][current_record_item]
            break
            
    _update_file(recordsMovement)
    click.echo(click.style("record updated successfully", bg="green", fg="white", bold=True ))
    pass

@records.command()
@click.argument('movement_id', type=str)
def delete(movement_id):
    """Delete records"""
    recordsMovement = _get_movements()
    movement = _get_movement(recordsMovement, movement_id)
    
    if movement == None:
        click.echo(click.style('Insert valid movement', bg='red', fg='white', bold=True))
        return
    
    _get_record_history_movement(movement)
    
    record_id = click.prompt('Insert Number of Record you want to Delete', type=int, default=None)
    current_record_item = record_id -1
    if click.confirm('Are you sure you want to delete a {name} Record ({id})'.format(id=record_id, name=movement['name'])):
        for movement_item in recordsMovement:
            if movement_item['id'] == movement_id:
                del movement_item['records'][current_record_item]
                break

    _update_file(recordsMovement)
    click.echo(click.style("record deleted successfully", bg="green", fg="white", bold=True ))
    pass

@records.command()
def movements():
    """Movements lists"""
    recordsMovement = _get_movements()
    _print_movements(recordsMovement)

#private functions
@click.pass_context
def _get_movements(ctx):
    record_service = RecordService(ctx.obj['records_table'])
    return record_service.lists()

def _get_movement(movements, movement_id):
    movement = [movement for movement in movements if movement['id'] == movement_id]
    if len(movement) == 0:
        return None
    return movement[0]

def _print_movements(movements):
        for index, movement in enumerate(movements):
            position = index + 1
            click.echo('{i}.- [{id}] {name}'.format(i=position, id=movement['id'], name=movement['name']))
            click.echo(click.style('-' * 50, fg='green'))

def _get_record_percentages_movement(movement):
    percentages = _calc_percentages(movement['records'][-1]['weigth'])

    click.echo(click.style('{movement_name} percentages Lists, the weigth of your las PR is {weight}'.format(movement_name = movement['name'].upper(), weight = movement['records'][-1]['weigth']), bg='black', fg='white', bold=True))
    click.echo(click.style('% | WEIGTH ', fg='yellow', bold=True))
    click.echo(click.style('*' * 30, fg='green'))

    _print_percentages(percentages)
    pass

def _get_record_history_movement(movement):
    click.echo(click.style('{movement_name} History PR:'.format(
        movement_name = movement['name'].upper(),
        weight = movement['records'][-1]['weigth']), bg='black', fg='white', bold=True))
    click.echo(click.style('WEIGTH | DATE | REPETITIONS', fg='yellow', bold=True))
    
    for index, record in enumerate(movement['records']):
        click.echo('{index}.- {weigth} | {Date} | {Reps}'.format(
            weigth=record['weigth'],
            Date=record['date'],
            Reps = record['repetitions'],
            index= index +1
        ))
        click.echo(click.style('-' * 20, fg='green'))
    pass

def _calc_percentages(weigth):
    percentages = []
    MIN_PERCENTAgE = 5
    MAX_PERCENTAgE = 105
    
    for i in range(MIN_PERCENTAgE, MAX_PERCENTAgE, 5):
        percentages.append({
            'tag' : i,
            'value': int(weigth) * i // 100
        })
    return percentages

def _print_percentages(percentages):
        for percentage in percentages:
            click.echo('{percentage} % | {weigth} LBS'.format(percentage=percentage['tag'], weigth=percentage['value']))
            click.echo(click.style('-' * 20, fg='green'))

@click.pass_context
def _update_file(ctx, movements):
        record_service = RecordService(ctx.obj['records_table'])
        records = Record(movements)
        record_service.create(records)

all = records