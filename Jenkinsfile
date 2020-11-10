// https://stackoverflow.com/questions/51648534/unable-to-pip-install-in-docker-image-as-agent-through-jenkins-declarative-pipel?noredirect=1#comment90322558_51648534

pipeline {
    agent { docker {
        image 'python:3.8.5-slim'
        args '--volume /var/jenkins_dist/vocabulary-lib:/imported_dist/vocabulary-lib --volume /var/jenkins_dist/vocabulary-srv:/dist_output'
    } }
    stages {
        stage('Build') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'pip install /imported_dist/vocabulary-lib/main/vocabulary_RR-0.1-py3-none-any.whl'
                    sh 'pip install --editable .'
                }

            }
        }
        stage('Test') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'pip install pytest coverage'
                    sh 'python -m coverage run --source vocabulary_mgr,vocabulary_srv -m pytest'
                    sh 'python -m coverage report'

                }
            }
        }
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
                sh 'mkdir -p /dist_output/$GIT_BRANCH'
                sh 'rm -f /dist_output/$GIT_BRANCH/*'
                sh 'cp dist/*.whl /dist_output/$GIT_BRANCH/'
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}