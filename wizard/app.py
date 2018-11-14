import gc

import picoweb

from .nodes import nodes as _nodes


app = picoweb.WebApp(__name__)


_db = {
    'wifi_name': '',
    'wifi_pass': '',
    'mqtt_broker': '',
    'mqtt_user': '',
    'mqtt_pass': '',
    'mqtt_topic': 'homie',
    'device_name': 'mydevice',
    'nodes': {},
}

_pins = {5: "D1", 4: "D2",  0: "D3", 2: "D4", 14: "D5", 12: "D6", 13: "D7", 15: "D10"}


def render_template_to_file(fun, tmpl_name, args=()):
    tmpl = fun(tmpl_name)
    filename = '/{}.py'.format(tmpl_name.rstrip('.tmpl'))

    with open(filename, 'w') as f_out:
        for s in tmpl(*args):
            f_out.write(s)


@app.route('/',  methods=['GET', 'POST'])
def setup(request, response):
    gc.collect()

    global _db
    notify = None

    # first settings page
    page = 'w'

    if request.method == 'POST':
        yield from request.read_form_data()
        form = request.form
        page = form['n'][0]

        # wifi setup
        if form['t'][0] == 'w':
            _db['wifi_name'] = form['wn'][0]
            _db['wifi_pass'] = form['wp'][0]

        # mqtt setup
        elif form['t'][0] == 'm':
            _db['mqtt_broker'] = form['mb'][0]
            _db['mqtt_user'] = form['mu'][0]
            _db['mqtt_pass'] = form['mp'][0]
            _db['mqtt_topic'] = form['mt'][0]

        # device setup
        elif form['t'][0] == 'd':
            _db['device_name'] = form['dn'][0]
            if 'nds' in form:
                # delete nodes not in form
                for node in _db['nodes']:
                    if node not in form['nds']:
                        del _db['nodes'][node]
                # add nodes from form to _db
                for node in form['nds']:
                    if node not in _db['nodes']:
                        p = _nodes[node]['pin']['default']
                        if isinstance(p, int):
                            p = [p]
                        _db['nodes'][node] = {
                            "pin": p,
                            "interval": _nodes[node]['pin']['default'],
                        }

        # node setup
        elif form['t'][0] == 'n':
            pins = []
            for node in _db['nodes']:
                if 'pin' in _db['nodes'][node]:
                    p = [int(x) for x in form[node]]
                    _db['nodes'][node]['pin'] = p
                    _db['nodes'][node]['map'] = [_pins[x] for x in p]
                    pins.extend(_db['nodes'][node]['pin'])
                elif 'url' in _db['nodes'][node]:
                    _db['nodes'][node]['url'] = form[node][0]
            if page == 'f':
                if len(pins) != len(set(pins)):
                    page = 'n'
                    notify = 'You can\'t use a pin twice.'

    if page == 'end':
        # write settings.py
        render_template_to_file(
            app._load_template, 'settings.tmpl', (_db,))
        # write main.py
        render_template_to_file(
            app._load_template, 'main.tmpl', (_db['nodes'],))

    yield from picoweb.start_response(response)
    yield from app.render_template(response, 'index.html',
                                   (_db, page, _nodes, notify))


# Send style.css and add cache header
@app.route('/style.min.css', methods=['GET'])
def style(request, response):
    headers = b'Cache-Control: max-age=86400\r\n'
    yield from app.sendfile(response, 'static/style.min.css',
                            'text/css', headers)


def preload_templates():
    # Preload templates to avoid memory fragmentation issues
    app._load_template('index.html')
    app._load_template('settings.tmpl')
    app._load_template('main.tmpl')


def main():
    preload_templates()
    gc.collect()
    print("\nSetup wizard listen on http://192.168.4.1")
    app.run(host='0.0.0.0', port=80, debug=-1)


if __name__ == "__main__":
    main()
