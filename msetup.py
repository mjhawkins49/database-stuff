#!/usr/bin/env python
#import random

import score
import hood
import coll

def clean():
    score.drop_score_table()
    hood.drop_hood_table()
    coll.drop_coll_table()

def create():
    score.create_score_table()
    hood.create_hood_table()
    coll.create_coll_table()

def setup():
    clean()
    create()

    mikeId = coll.insert_coll({
        coll.COL_NAME: 'Sam',
        coll.COL_GENDER: 'M',
        coll.COL_AGE: 49
    })

    sallyId = coll.insert_coll({
        coll.COL_NAME: 'Sally',
        coll.COL_GENDER: 'F',
        coll.COL_AGE: 33
    })
    mikeId = coll.insert_coll({
        coll.COL_NAME: 'Jasper',
        coll.COL_GENDER: 'M',
        coll.COL_AGE: 23
    })

    sallyId = coll.insert_coll({
        coll.COL_NAME: 'Jasmine',
        coll.COL_GENDER: 'F',
        coll.COL_AGE: 21
    })
    redlandsId = hood.insert_hood({
        hood.COL_NAME: 'Redlands'
    })

    cliftonId = hood.insert_hood({
        hood.COL_NAME: 'Orchard Mesa'
    })
    redlandsId = hood.insert_hood({
        hood.COL_NAME: 'Clifton'
    })

    cliftonId = hood.insert_hood({
        hood.COL_NAME: 'Palisade'
    })
    redlandsId = hood.insert_hood({
        hood.COL_NAME: 'Downtown'
    })

    cliftonId = hood.insert_hood({
        hood.COL_NAME: 'Fruita'
    })

    #for test in range(10):
       # if test % 2 in [0,1]:
        #    collId = mikeId
       # else:
       #     collId = sallyId
       # if test % 2 in [0,2]:
       #     hoodId = redlandsId
       # else:
       #     hoodId = cliftonId
       # mentalscore = random.randint(1,5)
       # score.insert_score({
         #   score.COL_SCORE: mentalscore,
          #  score.COL_HOOD_ID: hoodId,
          #  score.COL_COLL_ID: collId
        #})

if __name__ == '__main__':
    print ('setup()')
    setup()