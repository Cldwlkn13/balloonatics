
def custom_formset_dictionary_parser(requestDictionary):
    d = {}
    for i in requestDictionary:
        k = i.split('=')[0]
        v = i.split('=')[1] 
        if 'form' in k:    
            d[k] = v

    s = {}
    f = 0
    for k, v in d.items():
        if 'product' in k:
            g = {}
            g['product'] = v
            s[f] = g
            f += 1

    f = 0
    for k, v in d.items():
        if 'item_qty' in k:
            s[f]['item_qty'] = v
            f += 1
    
    return s