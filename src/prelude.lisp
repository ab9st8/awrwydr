% These are some useful definitions that are parsed and loaded by the interpreter
% before the REPL prompt comes up.

% Extended cons utilites
(define caar (λ (val)
    (car (car val))))

(define cddr (λ (val)
    (cdr (cdr val))))

(define cadr (λ (val)
    (car (cdr val))))

(define cdar (λ (val)
    (cdr (car val))))

(define cons? (λ (val)
    (not? (or? (atom? val) (nil? val)))))

% Boolean operators and utilities
% ~
% Keep in mind that as these are Awrwydr definitions
% there's no actual type-checking being done lol
(define not? (lambda (a)
    (cond
        (a false)
        (true true))))

(define or? (lambda (a b)
    (cond
        (a true)
        (b true)
        (true false))))

(define and? (lambda (a b)
    (cond
        ((eq? (list true true) (list a b)) true)
        (true false))))

% Defined in the Paper, p.12
(define ff (λ (val)
    (cond
        ((atom? val) val)
        (true (ff (car val))))))

% Defined in the Paper, p.14
(define among (λ (list el)
    (cond
        ((cons? list) (or? (among (car list) el) (among (cdr list) el)))
        (true (eq? list el)))))