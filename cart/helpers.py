from products.models import Product

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

def validate_bundle_item_products(bundle_item_dict):
    product_ids = []
    valid = False
    for k, item in bundle_item_dict.items(): 
        if item['product'] != '0':
            product = Product.objects.get(pk=item['product'])
            if product.id in product_ids:
                return { 'is_valid': False, 'product': product }
            product_ids.append(product.id)
            valid = True # set when at least one item valid (i.e. cannot validate 0 bundle items) 
    return {'is_valid': valid, 'product': None }


def validate_bundle_item_qtys(bundle_item_dict):
    for k, item in bundle_item_dict.items(): 
        if item['product'] != '0':
            product = Product.objects.get(pk=item['product'])
            if (int(item['item_qty']) > product.qty_held or 
                int(item['item_qty']) == 0):
                return { 'is_valid': False, 'product': product }
    return { 'is_valid': True }


def save_bundle_items(bundle_item_dict, bundle): 
    for k, item in bundle_item_dict.items():
        if item['product'] != '0':
            product = Product.objects.get(pk=item['product'])
            bundle_item = BundleItem(
                product=product,
                bundle=bundle,
                item_qty=int(item['item_qty'])
            )
            bundle_item.save()


def get_bundle_item_dictionary(request_body):
    requestDictionary = request_body.decode("utf-8").split('&')
    return custom_formset_dictionary_parser(requestDictionary)


def getCannotProcessMessageProducts(product):
    msg = ''
    if product: 
        msg = f'''
            Invalid configuration of products, 
            more than one {product.name} 
            present in the bundle. 
            Please adjust your selections.
            '''
    else:
        msg = f'''
            No valid products in your bundle. 
            Please try again.
            '''
    return msg


def getCannotProcessMessageQtys(product):
    msg = ''
    if product.qty_held == 0:
        msg = f'''
        Sorry! We could not update your bundle. 
        We currently have no item <strong>{ product.name }</strong> 
        in stock!
        Please replace it with an alternative product.'''
    else:
        msg = f'''
        Sorry! We could not update your bundle. 
        The qty of item <strong>{ product.name }</strong> 
        is too high! 
        We only have { product.qty_held } in stock.'''
        
    return msg