// https://stackoverflow.com/questions/51648534/unable-to-pip-install-in-docker-image-as-agent-through-jenkins-declarative-pipel?noredirect=1#comment90322558_51648534

pipeline {
    agent { docker {
        image 'python:3.8.5-slim'
        args '--volume /var/jenkins_dist/vocabulary-lib:/dist/vocabulary-lib,/var/jenkins_dist/vocabulary-srv:/dist/vocabulary-srv'
    } }
    stages {
        stage('Build') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'pip freeze'
                    sh 'pip install --force-reinstall --user /dist/vocabulary-lib/vocabulary_RR-0.1-py3-none-any.whl'
                    sh 'pip install --force-reinstall --user --editable .'
                }

            }
        }
        stage('Test') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'pip freeze'
                    sh 'pip install pytest coverage'
                    sh 'coverage run --source vocabulary_mgr,vocabulary_srv  -m pytest'
                    sh 'coverage report'

                }
            }
        }
        /*
        stage('Packaging') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'id'
                    sh 'pip install --upgrade setuptools wheel'
                    sh 'python setup.py sdist bdist_wheel'
                }
            }
        }
        stage('Saving package') {
            steps {
                sh 'id'
                sh 'ls -la /dist_persistent'
                sh 'rm -f /dist_persistent/*'
                sh 'cp dist/*.whl /dist_persistent/'
            }
        }
        */
    }
}