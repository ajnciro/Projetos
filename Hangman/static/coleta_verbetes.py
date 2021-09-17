import funcoes as f

f.create_table('verbetes')
#f.limpa_tabela('verbetes')

tit = []
conta_ver = 0

#realiza a coleta de verbetes desejáveis da Wikipédia
while conta_ver < 2000:
    try:
        with f.urllib.request.urlopen("https://pt.wikipedia.org/wiki/Especial:Aleat%C3%B3ria") as url:
            page = url.read()
            soup = f.BeautifulSoup(page, "html.parser")
            try:
                sp = soup.p.get_text()
                
            except:
                print('erro (1)!!!')
                
        sep = " –"
        tit = f.re.split(sep, soup.title.string)[0]
        strin = f.replace_list(sp, '(?=\[).+?(?<=\])', '')
        strin = strin.replace(tit,tit.upper())
        strin = strin.replace(tit.upper(),f.pattern(len(tit)))
        
        
        if (tit.isalpha() and (tit in sp) and (tit == f.unidecode (tit)) and len(set(tit))<=10):
            print (tit, len(tit), strin)
            
            f.data_insert('verbetes',tit, len(tit), strin)
            
            conta_ver+=1
            print ('=== {} ==='.format(conta_ver))
        
    except:
        print('erro (2)!!!')
        
f.close()