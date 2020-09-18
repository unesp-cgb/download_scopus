#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
import time
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError

ano = '2014'

scopusApiKey = 'COLOQUE_AQUI_SUA_CHAVE'
consulta = 'https://api.elsevier.com/content/search/scopus?query=affil(unesp)+and+pubyear+=+'+ano+''


q = Request(consulta + '&apiKey='+ scopusApiKey+'&count=0')
q.add_header('Accept', 'application/json')
data = json.loads(urlopen(q).read())

resultados = data['search-results']['opensearch:totalResults']
print ('Total: '+resultados+"\n")
pagina = 0
itensPorPagina = 200

while pagina < (int(resultados) / int(itensPorPagina)) + 1:
  print('Página '+str(pagina))
  start = pagina * itensPorPagina
  url = consulta + '&apiKey='+ scopusApiKey+'&start='+str(start)+'&count='+str(itensPorPagina)
  print(url)
  try: 
    q = Request(url)
    q.add_header('Accept', 'application/json')
    data = json.loads(urlopen(q).read())
    registros = data['search-results']['entry']
    for registro in registros:
      if not os.path.exists('scopus_'+ano+'/'+registro['eid']+'.xml'):
        q = Request(registro['prism:url'] + '?apiKey='+ scopusApiKey)
        q.add_header('Accept', 'application/xml')
        nomeArquivoXmlPreprocessado = 'scopus_'+ano+'/'+registro['eid']+'.xml'
        arquivoXML = open(nomeArquivoXmlPreprocessado,'wb')
        arquivoXML.write(urlopen(q).read())
        arquivoXML.close()
        time.sleep( 2 )
    pagina = pagina + 1
  except HTTPError as e:
    error_message = e.read()
    print (error_message)
