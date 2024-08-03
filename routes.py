from db_connection import get_all_data, get_table_data, add_table_data, update_table_data, delete_table_data
import urllib.parse


def handle_homepage(handler, _):
    res = get_all_data()
    context = {
        'table_list': ''.join(
            f'<tr><td>{table}</td><td><a href="/{table}">Manage Table</a></td></tr>' for table in res
        )
    }
    handler._set_response()
    handler._serve_template('homepage.html', context)


def handle_query_table(handler, params):
    column_names, res = get_table_data(params['table_name'])
    context = {
        'table_name': params['table_name'],
        'table_columns': ''.join(f'<th>{col}</th>' for col in column_names),
        'table_data': ''.join(
            f'<tr data-id="{row[0]}">'
            f'{"".join(f"<td><span>{row[i]}</span><input type=\'text\' name=\'{col}\' value=\'{
                       row[i]}\' style=\'display:none;\'></td>" for i, col in enumerate(column_names))}'
            f'<td><button class="edit-btn">Edit</button><button class="save-btn" style="display:none;">Save</button>'
            f'<a href="/{params["table_name"]
                         }/delete?id={row[0]}">Delete</a></td>'
            f'</tr>'
            for row in res
        ),
        'table_form': ''.join(
            f'<input type="text" name="{col}" placeholder="{col}">' for col in column_names if col != 'id'
        )
    }
    handler._set_response()
    handler._serve_template('table.html', context)


def handle_add_table_data(handler, params):
    length = int(handler.headers['Content-Length'])
    post_data = urllib.parse.parse_qs(
        handler.rfile.read(length).decode('utf-8'))
    table_name = params['table_name']
    data = {key: value[0] for key, value in post_data.items()}
    add_table_data(table_name, data)
    handler.send_response(303)
    handler.send_header('Location', f'/{table_name}')
    handler.end_headers()


def handle_edit_table_data(handler, params):
    length = int(handler.headers['Content-Length'])
    post_data = urllib.parse.parse_qs(
        handler.rfile.read(length).decode('utf-8'))
    table_name = params['table_name']
    data = {key: value[0] for key, value in post_data.items()}
    item_id = data.pop('id')
    update_table_data(table_name, data, f"id = {item_id}")
    handler.send_response(303)
    handler.send_header('Location', f'/{table_name}')
    handler.end_headers()


def handle_delete_table_data(handler, params):
    item_id = handler.path.split('?')[1].split('=')[1]
    table_name = params['table_name']
    delete_table_data(table_name, f"id = {item_id}")
    handler.send_response(303)
    handler.send_header('Location', f'/{table_name}')
    handler.end_headers()


ROUTE_TO_HANDLER = {
    r"/": handle_homepage,
    r"/(?P<table_name>(access_log|emergency_status|access_key|room|building|organization|privacy|user))": handle_query_table,
    r"/(?P<table_name>(access_log|emergency_status|access_key|room|building|organization|privacy|user))/add": handle_add_table_data,
    r"/(?P<table_name>(access_log|emergency_status|access_key|room|building|organization|privacy|user))/edit": handle_edit_table_data,
    r"/(?P<table_name>(access_log|emergency_status|access_key|room|building|organization|privacy|user))/delete": handle_delete_table_data,
}
