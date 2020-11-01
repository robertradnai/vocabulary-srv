// https://stackoverflow.com/questions/51648534/unable-to-pip-install-in-docker-image-as-agent-through-jenkins-declarative-pipel?noredirect=1#comment90322558_51648534

pipeline {
    agent { docker {
        image 'python:3.8.5-slim'
        args '--volume /var/jenkins_dist/vocabulary-lib:/dist/vocabulary-lib'
    } }
    stages {
        stage('Build') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'pip install /dist/vocabulary-lib/vocabulary_RR-0.1-py3-none-any.whl'
                    sh 'pip install --user --editable .'
                }

            }
        }
        stage('Test') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    dir('tests') {
                        sh 'pytest'
                    }
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