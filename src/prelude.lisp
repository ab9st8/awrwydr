;; These are some useful definitions that are parsed and loaded by the interpreter
;; before the REPL prompt comes up. 


(define caar (λ (val)
    (car (car val))))

(define cddr (λ (val)
    (cdr (cdr val))))

(define cadr (λ (val)
    (car (cdr val))))

(define cdar (λ (val)
    (cdr (car val))))

(define cons? (λ (val)
    (not? ((atom? val) (nil? val)))))

;; Defined in the Paper, p.12
(define ff (λ (val)
    (cond
        ((atom? val) val)
        (true (ff (car val))))))

;; Defined in the Paper, p.14
(define among (λ (list el)
    (cond
        ((cons? list) (or? (among (car list) el) (among (cdr list) el)))
        (true (eq? list el)))))

