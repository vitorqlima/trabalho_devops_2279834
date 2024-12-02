pipeline {
    agent any

    stages {
        stage('Preparar Ambiente') {
            steps {
                echo 'Preparando o ambiente...'
                script {
                    sh 'docker-compose down -v || true'
                }
            }
        }

        stage('Construir Contêineres') {
            steps {
                echo 'Construindo contêineres com Docker Compose...'
                script {
                    sh 'docker-compose up -d --build'
                }
            }
        }

        stage('Aguardar Banco de Dados') {
            steps {
                echo 'Aguardando o MariaDB estar pronto...'
                script {
                    sh '''
                    for i in {1..10}; do
                        if docker-compose exec mariadb mysqladmin ping -h localhost --silent; then
                            echo "MariaDB está pronto!"
                            exit 0
                        fi
                        echo "Aguardando MariaDB..."
                        sleep 5
                    done
                    echo "MariaDB não respondeu a tempo."
                    exit 1
                    '''
                }
            }
        }

        stage('Executar Testes') {
            steps {
                echo 'Executando os testes...'
                script {
                    sh 'docker-compose exec flask_app pytest --disable-warnings'
                }
            }
        }

        stage('Finalizar') {
            steps {
                echo 'Finalizando e limpando os recursos...'
                script {
                    sh 'docker-compose down -v'
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finalizado.'
            script {
                sh 'docker-compose down -v || true'
            }
        }

        success {
            echo 'Pipeline executado com sucesso.'
        }

        failure {
            echo 'O pipeline falhou.'
        }
    }
}
