// Enables GitHub push-based trigger (required for non-multibranch jobs)
properties([
  pipelineTriggers([
    [$class: 'GitHubPushTrigger']
  ])
])

pipeline {
  agent any

  stages {
    stage('Build') {
      steps {
        echo '🏗️ Dummy build step'
      }
    }
    stage('Scan') {
      steps {
        echo '🔍 Dummy scan step'
      }
    }
    stage('Dockerize') {
      steps {
        echo '🐳 Dummy docker step'
      }
    }
    stage('Deploy') {
      steps {
        echo '🚀 Dummy deploy step'
      }
    }
  }

  post {
    success {
      echo '✅ Pipeline completed successfully'
    }
    failure {
      echo '❌ Pipeline failed'
    }
  }
}

