#!flask/bin/python
import six
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()


pkts = [
        {'id': 1, 'protocolo': "http", 'tamanho': "elefante", 'duracao': "tartaruga", 'taxa': "caramujo"},
        {'id': 2, 'protocolo': "ssh", 'tamanho': "rato", 'duracao': "libelula", 'taxa': "guepardo"},
        {'id': 3, 'protocolo': "dhcp", 'tamanho': "elefante", 'duracao': "tartaruga", 'taxa': "caramujo"},
        {'id': 4, 'protocolo': "bittorrent", 'tamanho': "rato", 'duracao': "libelula", 'taxa': "guepardo"},
        {'id': 5, 'protocolo': "ssdp", 'tamanho': "elefante", 'duracao': "tartaruga", 'taxa': "caramujo"},
        {'id': 6, 'protocolo': "ssh", 'tamanho': "rato", 'duracao': "libelula", 'taxa': "guepardo"},
        {'id': 7, 'protocolo': "ssl", 'tamanho': "elefante", 'duracao': "tartaruga", 'taxa': "caramujo"},
        {'id': 8, 'protocolo': "dhcp", 'tamanho': "rato", 'duracao': "libelula", 'taxa': "guepardo"}
        ]


@auth.get_password
def get_password(username):
    if username == 'root':
        return 'rsi-psd'
    return None


@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/rest/api/pkts', methods=['GET'])
@auth.login_required
def get_pkts():
    return jsonify({'pkts': [make_public_pkt(pkt) for pkt in pkts]})


@app.route('/rest/api/pkts/<int:pkt_id>', methods=['GET'])
@auth.login_required
def get_pkt(pkt_id):
    pkt = [pkt for pkt in pkts if pkt['id'] == pkt_id]
    if len(pkt) == 0:
        abort(404)
    return jsonify({'pkt': make_public_pkt(pkt[0])})


@app.route('/rest/api/<string:protocolo>/tamanho', methods=['GET'])
@auth.login_required
def get_pkts_tamanho(protocolo):
    conta_elefante = 0
    conta_rato = 0
    pkts_tamanho = [pkt for pkt in pkts if pkt['protocolo'] == protocolo]
    if len(pkts_tamanho) == 0:
        abort(404)
    for pkt in pkts_tamanho:
        if pkt['tamanho']== 'elefante':
            conta_elefante += 1

        if pkt['tamanho']== 'rato':
            conta_rato += 1

    return jsonify({'%s por tamanho' % protocolo.upper(): 
        [{'Qtd Elefantes':conta_elefante}, {'Qtd Ratos':conta_rato},
        {'Pocentagem Elefantes':float(100*conta_elefante/(conta_elefante+conta_rato))}, 
        {'Pocentagem  Ratos':float(100*conta_rato/(conta_elefante+conta_rato))}]})


@app.route('/rest/api/<string:protocolo>/duracao', methods=['GET'])
@auth.login_required
def get_pkts_duracao(protocolo):
    conta_tartaruga = 0
    conta_libelula = 0
    pkts_duracao = [pkt for pkt in pkts if pkt['protocolo'] == protocolo]
    if len(pkts_duracao) == 0:
        abort(404)
    for pkt in pkts_duracao:
        if pkt['duracao']== 'tartaruga':
            conta_tartaruga += 1

        if pkt['duracao']== 'libelula':
            conta_libelula += 1

    return jsonify({'%s por duracao' % protocolo.upper(): 
        [{'Qtd Tartarugas':conta_tartaruga}, {'Qtd Libelulas':conta_libelula},
        {'Pocentagem Tartarugas':float(100*conta_tartaruga/(conta_tartaruga+conta_libelula))}, 
        {'Pocentagem  Libelulas':float(100*conta_libelula/(conta_tartaruga+conta_libelula))}]})


@app.route('/rest/api/<string:protocolo>/taxa', methods=['GET'])
@auth.login_required
def get_pkts_taxa(protocolo):
    conta_guepardo = 0
    conta_caramujo = 0
    pkts_taxa = [pkt for pkt in pkts if pkt['protocolo'] == protocolo]
    if len(pkts_taxa) == 0:
        abort(404)
    for pkt in pkts_taxa:
        if pkt['taxa']== 'guepardo':
            conta_guepardo += 1

        if pkt['taxa']== 'caramujo':
            conta_caramujo += 1

    return jsonify({'%s por taxa' % protocolo.upper(): 
        [{'Qtd Guepardos':conta_guepardo}, {'Qtd Caramujos':conta_caramujo},
        {'Pocentagem Guepardos':float(100*conta_guepardo/(conta_guepardo+conta_caramujo))}, 
        {'Pocentagem Caramujos':float(100*conta_caramujo/(conta_guepardo+conta_caramujo))}]})


@app.route('/rest/api/<string:animal>', methods=['GET'])
@auth.login_required
def get_animal(animal):
    conta_bittorrent = 0
    conta_dhcp = 0
    conta_http = 0
    conta_ssdp = 0
    conta_ssh = 0
    conta_ssl = 0

    pkts_animal = [pkt for pkt in pkts if pkt['tamanho'] == animal or pkt['duracao'] == animal or pkt['taxa'] == animal]
    if len(pkts_animal) == 0:
        abort(404)
    for pkt in pkts_animal:
        if pkt['protocolo']== 'bittorrent':
            conta_bittorrent += 1
        if pkt['protocolo']== 'dhcp':
            conta_dhcp += 1
        if pkt['protocolo']== 'http':
            conta_http += 1
        if pkt['protocolo']== 'ssdp':
            conta_ssdp += 1
        if pkt['protocolo']== 'ssh':
            conta_ssh += 1
        if pkt['protocolo']== 'ssl':
            conta_ssl += 1

    return jsonify({'%s por protocolo' % animal.upper(): 
            [
                {'Qtd bittorrent':conta_bittorrent}, {'Qtd dhcp':conta_dhcp},
                {'Qtd http':conta_http}, {'Qtd ssdp':conta_ssdp}, {'Qtd ssh':conta_ssh}, {'Qtd ssl':conta_ssl},
                {'Pocentagem bittorrent':float(100*conta_bittorrent/(conta_bittorrent+conta_dhcp+conta_http+conta_ssdp+conta_ssh+conta_ssl))},
                {'Pocentagem dhcp':float(100*conta_dhcp/(conta_bittorrent+conta_dhcp+conta_http+conta_ssdp+conta_ssh+conta_ssl))},
                {'Pocentagem http':float(100*conta_http/(conta_bittorrent+conta_dhcp+conta_http+conta_ssdp+conta_ssh+conta_ssl))},
                {'Pocentagem ssdp':float(100*conta_ssdp/(conta_bittorrent+conta_dhcp+conta_http+conta_ssdp+conta_ssh+conta_ssl))},
                {'Pocentagem ssh':float(100*conta_ssh/(conta_bittorrent+conta_dhcp+conta_http+conta_ssdp+conta_ssh+conta_ssl))}, 
                {'Pocentagem ssl':float(100*conta_ssl/(conta_bittorrent+conta_dhcp+conta_http+conta_ssdp+conta_ssh+conta_ssl))}
            ]
        })


def make_public_pkt(pkt):
    new_pkt = {}
    for field in pkt:
        if field == 'id':
            new_pkt['uri'] = url_for('get_pkt', pkt_id=pkt['id'],
                                      _external=True)
        else:
            new_pkt[field] = pkt[field]
    return new_pkt

if __name__ == '__main__':
    app.run(debug=True)
