pipeline {
    agent {
        kubernetes {
        yaml '''
apiVersion: v1
kind: Pod
metadata:
  labels:
    agent: jenkins-agent
  namespace: jenkins
spec:
  serviceAccountName: jenkins-agent # Enter the service account name being used
  securityContext:
        runAsUser: 0
        fsGroup: 0
        runAsNonRoot: false
  containers:
  - name: jenkins-agent
    image: 070682830013.dkr.ecr.us-east-1.amazonaws.com/jenkins-agent-dev:v1.8 # Enter the jenkins inbound agent image.
    command:
    - cat
    tty: true
    resources:
      requests:
        cpu: 100m
        memory: 256Mi
    volumeMounts:
    - mountPath: /var/run
      name: docker-sock-volume
  volumes:
    - name: docker-sock-volume
      hostPath:
        path: /var/run
        type: Directory
  tolerations:
  - key: "SERVICE"
    operator: "Equal"
    value: "JENKINS-AGENT"
    effect: "NoSchedule"
  nodeSelector:
    role: eks-jenkins-agent
        '''
        defaultContainer 'jenkins-agent'
        }
    }

    options {
        disableConcurrentBuilds()
    }

    environment {
        SONAR_PROJECT_DEV="fantasy-python-dev"
        SONAR_PROJECT_PROD="fantasy-python-prod"
        IMAGE_REGISTRY_DEV="fantasy-python-de-dev"
        IMAGE_REGISTRY_PROD="fantasy-python-de-prod"
        K8S_MANIFESTS_BRANCH_DEV="fantasy-python-dev"
        K8S_MANIFESTS_BRANCH_PROD="fantasy-python-prod"  
        REPO_URL="https://github.com/Moh-Tarek/fantasy.git"
    }

    stages {
        stage('Setting-up variables') {
            steps {
                script{
                    if (env.GIT_BRANCH == 'develop') {
                        env.SONAR_PROJECT=env.SONAR_PROJECT_DEV
                        env.IMAGE_REGISTRY=env.IMAGE_REGISTRY_DEV
                        env.K8S_MANIFESTS_BRANCH=env.K8S_MANIFESTS_BRANCH_DEV
                    } else if (env.GIT_BRANCH == 'master'){
                        env.SONAR_PROJECT=env.SONAR_PROJECT_PROD
                        env.IMAGE_REGISTRY=env.IMAGE_REGISTRY_PROD
                        env.K8S_MANIFESTS_BRANCH=env.K8S_MANIFESTS_BRANCH_PROD
                    }else{
                        currentBuild.result = 'FAILURE'
                        error("Branch is not configured")
                    }
                }
            }
        }


        stage('Getting Repo files') {
            steps {
                git branch: "${GIT_BRANCH}", credentialsId: 'github_credentials_devops', url: "${env.REPO_URL}"
            }
        }

        stage('Pulling K8S Deployment Files') {
            steps {
                dir('k8s') {
                    git branch: "${env.K8S_MANIFESTS_BRANCH}", credentialsId: 'gitlab_credentials_devops', url: 'https://gitlab.nagwa.com/devops/k8s_manifests.git'
                }
                
            }
        }

        stage('Build and Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'azure-nugets-aya', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh '''
                        export COMMIT_COUNT=$(git rev-list --count HEAD)
                        export SHORT_HASH=$(git rev-parse --short HEAD)
                        export TAG=${COMMIT_COUNT}.${SHORT_HASH}
                        export REPO="070682830013.dkr.ecr.us-east-1.amazonaws.com/${IMAGE_REGISTRY}"
                        aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 070682830013.dkr.ecr.us-east-1.amazonaws.com
                        docker build --network host --build-arg USERNAME=\"${USERNAME}\" --build-arg PASSWORD=\"${PASSWORD}\" -t ${REPO}:${TAG} .
                        docker push ${REPO}:${TAG}
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                export COMMIT_COUNT=$(git rev-list --count HEAD)
                export SHORT_HASH=$(git rev-parse --short HEAD)
                export TAG=${COMMIT_COUNT}.${SHORT_HASH}
                export REPO="070682830013.dkr.ecr.us-east-1.amazonaws.com/${IMAGE_REGISTRY}"
                python3 k8s/env.py
                sed -i.bak "s|IMAGE_NAME|${REPO}:${TAG}|g" k8s/deployment.yaml
                kubectl apply -f k8s/secrets.yaml
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml
                kubectl apply -f k8s/ingress.yaml
                '''
            }
        }
    }
    post {
        // success {
        //     office365ConnectorSend webhookUrl: "https://chestnut100.webhook.office.com/webhookb2/e2c9bec3-1678-4d53-a212-d5b03e7e30a0@474d89ff-edef-480c-8822-c4da6bfcadf2/JenkinsCI/4a947d542e3548b49ec6474dc1fef158/e38604be-2f87-4f1a-a6c3-32c04f5e4dc6",
        //     color: '#00FF00',
        //     message: "SUCCESSFUL",
        //     status: 'Success' 
        // }
         
        // failure {
        //     office365ConnectorSend webhookUrl: "https://chestnut100.webhook.office.com/webhookb2/e2c9bec3-1678-4d53-a212-d5b03e7e30a0@474d89ff-edef-480c-8822-c4da6bfcadf2/JenkinsCI/4a947d542e3548b49ec6474dc1fef158/e38604be-2f87-4f1a-a6c3-32c04f5e4dc6",
        //     color: '#FF0000',
        //     message: "FAILED",
        //     status: 'Success' 
        // }

        cleanup{
            cleanWs()
        }     
    }
}
