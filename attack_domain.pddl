(define (domain attack)

    (:predicates
        (attacker ?a) (computer ?c) (connected-to ?x ?y) (controlled-by ?c ?a) (is-windows7 ?c) (is-windows10 ?c) (is-ubuntu16 ?c) (is-mint ?c)
    )

    (:action attack-windows7
        :parameters ( ?a ?c1 ?c2)
        :precondition (and (attacker ?a) (computer ?c1) (computer ?c2) (not (controlled-by ?c2 ?a)) (controlled-by ?c1 ?a) (connected-to ?c1 ?c2 ) 
             (is-windows7 ?c2))
        :effect (and (controlled-by ?c2 ?a))
    )
    
    (:action attack-windows10
        :parameters ( ?a ?c1 ?c2)
        :precondition (and (attacker ?a) (computer ?c1) (computer ?c2) (not (controlled-by ?c2 ?a)) (controlled-by ?c1 ?a) (connected-to ?c1 ?c2 ) 
             (is-windows10 ?c2))
        :effect (and (controlled-by ?c2 ?a))
    )
    
    (:action attack-ubuntu16
        :parameters ( ?a ?c1 ?c2)
        :precondition (and (attacker ?a) (computer ?c1) (computer ?c2) (not (controlled-by ?c2 ?a)) (controlled-by ?c1 ?a) (connected-to ?c1 ?c2 ) 
             (is-ubuntu16 ?c2))
        :effect (and (controlled-by ?c2 ?a))
    )
    
    (:action attack-mint
       :parameters ( ?a ?c1 ?c2)
        :precondition (and (attacker ?a) (computer ?c1) (computer ?c2) (not (controlled-by ?c2 ?a)) (controlled-by ?c1 ?a) (connected-to ?c1 ?c2 ) 
             (is-mint ?c2))
        :effect (and (controlled-by ?c2 ?a))
    )
    
)
