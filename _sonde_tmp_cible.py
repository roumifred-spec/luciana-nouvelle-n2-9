import ast
src = open('luciana.py', encoding='utf-8').read()
arbre = ast.parse(src)
n = [x for x in ast.walk(arbre) if isinstance(x, ast.FunctionDef) and x.name == '_repondre_tour'][0]
print('def _repondre_tour:', n.lineno, '->', n.end_lineno)
entete, blocs, msg, db = [], [], [], []
for x in ast.walk(n):
    if isinstance(x, ast.Name) and x.id == 'entete' and isinstance(x.ctx, ast.Load):
        entete.append(x.lineno)
    if isinstance(x, ast.Name) and x.id == 'detail_biblio':
        db.append(x.lineno)
    if isinstance(x, ast.Assign):
        for c in x.targets:
            if isinstance(c, ast.Name) and c.id == 'blocs_systeme':
                blocs.append(x.lineno)
            if isinstance(c, ast.Subscript) and isinstance(c.value, ast.Name) and c.value.id == 'messages':
                msg.append(x.lineno)
print('blocs_systeme   :', sorted(set(blocs)))
print('messages[..] =  :', sorted(set(msg)))
print('entete (lue)    :', sorted(set(entete)))
print('detail_biblio   :', sorted(set(db)))
