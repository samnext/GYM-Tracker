import pytest
from app.services.exercise import ExerciseService, ExerciseNotFound, ExerciseSchema
from app.models.base import ExerciseORM


def test_get_exercise_by_id_raises_exception(exercise_service):
    
    exercise_service.exercise_repository.get_by_id.return_value = None

    with pytest.raises(ExerciseNotFound):
        exercise_service.get_exercise_by_id(1)

    exercise_service.exercise_repository.get_by_id.assert_called_once_with(1)
        
def test_get_exercise_by_id_returns_schema_when_found(exercise_service):

    exercise_data = {
        "id":1,
        "name":"test",
        "description":"test",
        "category":"test",
        "muscle_group":"test"
    }
    exercise_orm = ExerciseORM(**exercise_data)

    exercise_service.exercise_repository.get_by_id.return_value = exercise_orm
    response_service = exercise_service.get_exercise_by_id(1)

    assert response_service.model_dump() == exercise_data

    exercise_service.exercise_repository.get_by_id.assert_called_once_with(1)

def test_get_all_exercises_returns_empty_list(exercise_service):

    #Arrange
    exercise_service.exercise_repository.get_all.return_value = []

    #Act
    response_service = exercise_service.get_all_exercises()

    #Assert
    assert response_service['total'] == 0
    assert response_service['items'] == []

    exercise_service.exercise_repository.get_all.assert_called_once_with()

def test_get_all_exercises_returns_full_list(exercise_service):

    exercise_data_1 = {
        "id":1,
        "name":"bench press",
        "description":"do bench press",
        "category":"press",
        "muscle_group":"chest"
    }
    exercise_data_2 = {
        "id":2,
        "name":"triceps extension",
        "description":"do triceps extension",
        "category":"extension",
        "muscle_group":"triceps"
    }
    exercise_data_tuple = (exercise_data_1, exercise_data_2)

    exercise_orms = [
        ExerciseORM(**exercise_data)
        for exercise_data in exercise_data_tuple
    ]

    exercise_service.exercise_repository.get_all.return_value = exercise_orms

    response_service = exercise_service.get_all_exercises()

    assert response_service['total'] == 2
    assert response_service['items'] == [
        ExerciseSchema(**exercise_data) 
        for exercise_data in exercise_data_tuple
    ]

    exercise_service.exercise_repository.get_all.assert_called_once_with()



        

        
        



    