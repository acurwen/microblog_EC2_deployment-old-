pipeline {
  agent any
    stages {
        stage ('Build') {
            steps {
                sh '''#!/bin/bash
                /* Creating virtual environment */
                python3.9 -m venv venv

                /* activate virtual environment */
                source venv/bin/activate

                /* install and upgrade python package manager */
                pip install pip --upgrade
                
                /* install all dependencies */
                pip install -r requirements.txt
                pip install gunicorn pymysql cryptography
                
                /* setting environmental variables */
                FLASK_APP=microblog.py
                
                /* setting up databases and compiling translation files */
                flask translate compile
                flask db upgrade
                '''
            }
        }
        stage ('Test') {
            steps {
                sh '''#!/bin/bash
                source venv/bin/activate
                py.test ./tests/unit/ --verbose --junit-xml test-reports/results.xml
                '''
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
      stage ('OWASP FS SCAN') {
            steps {
                dependencyCheck additionalArguments: '--scan ./ --disableYarnAudit --disableNodeAudit', odcInstallation: 'DP-Check'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }
      stage ('Clean') {
            steps {
                sh '''#!/bin/bash
                if [[ $(ps aux | grep -i "gunicorn" | tr -s " " | head -n 1 | cut -d " " -f 2) != 0 ]]
                then
                ps aux | grep -i "gunicorn" | tr -s " " | head -n 1 | cut -d " " -f 2 > pid.txt
                kill $(cat pid.txt)
                exit 0
                fi
                '''
            }
        }
      stage ('Deploy') {
            steps {
                sh '''#!/bin/bash
                /* activate virtual environment */
                source venv/bin/activate
            
                /* start gunicorn and the app */
                gunicorn -b :5000 -w 4 microblog:app
                '''
            }
        }
    }
}
