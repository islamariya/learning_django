import json

from graphene_django.utils.testing import GraphQLTestCase

from learning_platform.schema import schema


class GQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def test_all_courses_query(self):
        response = self.query(
            '''
            query {
                allCourses{
                            title
                            shortDescription
                            price
                            duration
            }
            }
            ''',
            op_name='allCourses'
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_retrieve_course_query(self):
        response = self.query(
            '''
            query {
                    retrieveCourse(id:1)
                    {
                    title
                    category{title}
                    shortDescription
                    version
                    duration
                    price
            }
            }
            ''',
            op_name='retrieveCourse'
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_all_lessons_in_course_query(self):
        response = self.query(
            '''
            query {
                   allLessonsInCourse(course:1)
                   {
                    sequenceNumber
                    title
                    description
                    course{title}
                    }
            }
            ''',
            op_name='allLessonsInCourse'
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_retrieve_lesson_query(self):
        response = self.query(
            '''
            query {
                   retrieveLesson(id:3)
                   {
                    course{title}
                    sequenceNumber
                    title
                    description
                    }
            }
            ''',
            op_name='retrieveLesson'
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_all_course_flows_query(self):
        response = self.query(
            '''
            query {
                   allCourseFlows
                   {
                    startDate
                    course{
                           title
                           duration
                           shortDescription
                           overview
                           price
                           }
                    }
            }
            ''',
            op_name='allCourseFlows'
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_retrieve_course_flow_query(self):
        response = self.query(
            '''
            query {
                   retrieveCourseFlow(id:1)
                   {
                    startDate
                    course{
                           title
                           duration
                           shortDescription
                           overview
                           price
                           }
                    }
            }
            ''',
            op_name='retrieveCourseFlow'
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_all_course_homework_query(self):
        response = self.query(
            '''
            query {
            allCourseHomework(courseFlow:1)
            {
                title
                sequenceNumber
                description
                courseFlow{course{title}}
                dueDate}
            }
            ''',
            op_name='allCourseHomework'
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_retrieve_course_homework_query(self):
        response = self.query(
            '''
            query {
            retrieveCourseHomework(id:3)
                {
                title
                sequenceNumber
                description
                dueDate
                courseFlow{course{title}}
                }
            }
            ''',
            op_name='retrieveCourseHomework'
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_course_timetable_query(self):
        response = self.query(
            '''
            query {
            courseTimetable(courseFlow:1)
                {
                date
                lesson{
                   title
                   description
                   }
                courseFlow{course{title}}
                }
            }
            ''',
            op_name='courseTimetable'
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_retrieve_course_flow_lesson_query(self):
        response = self.query(
            '''
            query {
              retrieveCourseFlowLesson(id:4)
              {
                  date
                  teacher{
                          firstName
                          lastName 
                          }
                  courseFlow{course{title}
                             startDate}
                  lesson{ 
                         title
                         description
                         sequenceNumber}
              }
            }
            ''',
            op_name='retrieveCourseFlowLesson'
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_all_students_enrolled_query(self):
        response = self.query(
            '''
            query {
                allStudentsEnrolled(courseFlow:1)
                    {student
                        {firstName
                        lastName
                        }
                    startLearningDate
                    }
            }
            ''',
            op_name='allStudentsEnrolled'
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_all_students_homework_query(self):
        response = self.query(
            '''
            query {
            allStudentsHomework(courseFlow:1, student:1)
                {student
                    {student
                        {firstName 
                        lastName
                        } 
                    }
                courseFlow
                    {course{title}
                startDate
                }
                homework{
                    title
                    dueDate
                    }
                status
                content
                dateOfCompletion
                teacherComments
                }
            }
            ''',
            op_name='allStudentsHomework'
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_retrieve_student_homework_query(self):
        response = self.query(
            '''
            query {
            retrieveStudentHomework(id:1)
                {student
                    {student
                        {firstName 
                        lastName
                        } 
                    }
                courseFlow
                    {course{title}
                startDate
                }
                homework{
                    title
                    dueDate
                    }
                status
                content
                dateOfCompletion
                teacherComments
                }
            }
            ''',
            op_name='retrieveStudentHomework'
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)