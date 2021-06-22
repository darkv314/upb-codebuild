import json
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

users_table = os.environ['USERS_TABLE']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(users_table)
records ={}

def getMovieInfo(event, context):
    path = event["path"]
    print(json.dumps(event))
    queryStringParameters = json.dumps(event["queryStringParameters"])
    if queryStringParameters == "null":
        movie_id = path.split("/")[-1]
        response = table.get_item(
        Key={
                'pk': movie_id,
                'sk': 'info'
            }
        )
        item = response['Item']
        return {
            'statusCode': 200,
            'body': json.dumps(item)
            }
    else:
        date = event["queryStringParameters"]["date"]
        response = table.scan(
            FilterExpression=Attr('sk').begins_with(date) & Attr('pk').eq(movie_id)
        )
        items = response['Items']
        return {
            'statusCode': 200,
            'body': json.dumps(items)
            }
        
    
def putMovieInfo(event, context):
    path = event['path']
    movie_id = path.split("/")[-1]
    body = json.loads(event['body'])
    queryStringParameters = json.dumps(event["queryStringParameters"])
    if queryStringParameters == "null":
        table.put_item(
          Item={
                'pk': movie_id,
                'sk': 'info',
                'title': body["title"],
                'main_actor': body["main_actor"],
                'year': body["year"]
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Movie record saved!')
        }
    else:
        date = event["queryStringParameters"]["date"]
        if not date in records:
            records[date] = 1
        else: 
            records[date] += 1
        table.put_item(
          Item={
                'pk': movie_id,
                'sk': date+"_sch"+str(records[date]),
                'schedule': body["schedule"],
                'cinema_room': body["cinema_room"]
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Movie date and schedule saved!')
        }
        
def getMoviePeople(event, context):
    path = event['path']
    movie_id = path.split("/")[-3]
    cinema_id = path.split("/")[-1]
    response = table.query(
        KeyConditionExpression=Key('pk').eq(movie_id+cinema_id))
    items = response['Items']
    return {
        'statusCode': 200,
        'body': json.dumps(items)
        }

def putPeopleOnMovie(event, context):
    path = event['path']
    movie_id = path.split("/")[-3]
    cinema_id = path.split("/")[-1]
    body = json.loads(event['body'])
    pk = movie_id + cinema_id;
    if not pk in records:
        records[pk] = 1;
    else:
        records[pk] += 1;
    table.put_item(
          Item={
                'pk': pk,
                'sk': 'person_'+records[pk],
                'name': body["name"],
                'ci': body["ci"]
            }
        )
    return {
        'statusCode': 200,
        'body': json.dumps('People on movie record saved!')
    }
    
def getCinemaInfo(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('gci w')
    }
    
def putCinemaInfo(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('pci w')
    }
    
def getPersonInfo(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('gpi w')
    }
    
def putPersonInfo(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('ppi w')
    }
