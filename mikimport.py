#!/usr/bin/env python

import mconfig
import csv
import score
import coll
import hood
import mfilters
import sys

def createRecord(row,db=mconfig.DB_NAME):
    print(f"createRecord({row})")
    collectorName = row['Collector']
    collectorRow=coll.select_coll_by_name(collectorName,db)
    if collectorRow == None:
        collectorId=coll.insert_coll({
            'name': collectorName},db)
    else:
        collectorId=collectorRow['id']
    locationName = row['Neighborhood']
    locationRow=hood.select_hood_by_name(locationName,db)
    if locationRow == None:
        raise ValueError(f"location {locationName} not in database.")
    locationId=locationRow['id']
    SurveyScore=mfilters.dbInteger(row['Response'])
    SurveySex=mfilters.dbString(row['Sex'])
    SurveyAge=mfilters.dbInteger(row['Age'])
    if SurveyScore < 0:
        raise ValueError(f"invalid score value.")
    scoreId=score.insert_score({
        score.COL_SCORE: SurveyScore,
        score.COL_SEX: SurveySex,
        score.COL_AGE: SurveyAge,
        score.COL_COLL_ID: collectorId, 
        score.COL_HOOD_ID : locationId},db)
    return (scoreId, collectorId, locationId)

def csvImport(csvFileName,db=mconfig.DB_NAME):
    with open(csvFileName) as csvFile:
        data = csv.DictReader(csvFile)
        for row in data:
            createRecord(row,db)

if __name__ == '__main__':
    for file in sys.argv[1:]:
        csvImport(file)