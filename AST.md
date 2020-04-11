```python
mod = Module(stmt* body, type_ignore *type_ignores)
    | Expression(expr body)
    | FunctionType(expr* argtypes, expr returns)
    
stmt = FunctionDef(identifier name, arguments args,
                stmt* body, expr* decorator_list, expr? returns,
                string? type_comment)
    | Return(expr? value)
    | Assign(expr* targets, expr value, string? type_comment)
    | AugAssign(expr target, operator op, expr value)
 
    | For(expr target, expr iter, stmt* body, stmt* orelse, string? type_comment)
    | While(expr test, stmt* body, stmt* orelse)
    | If(expr test, stmt* body, stmt* orelse)
    | Import(alias* names)
    | ImportFrom(identifier? module, alias* names, int? level)
    | Pass | Break | Continue

expr = NamedExpr(expr target, expr, value)
    | Compare(expr left, cmpop* ops, expr* comparators)
    | Call(expr func, expr* args, keyword* keywords)
    | Name(identifier id, expr_context ctx)

expr_context = Load | Store | Del | AugLoad | AugStore | Param

operator = Add | Sub | Mult | MatMult | Div | Mod | Pow

cmpop = Eq | NotEq | Lt | LtE | Gt | GtE | Is | IsNot | In | NotIn

keyword = (identifier? arg, expr value)

arguments = (arg* posonlyargs, arg* args, arg? vararg, arg* kwonlyargs,
            expr* kw_defaults, arg? kwarg, expr* defaults)

arg = (identifier arg, expr? annotation, string? type_comment)
      attributes (int lineno, int col_offset, int? end_lineno, int? end_col_offset)

alias = (identifier name, identifier? asname)
```