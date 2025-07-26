import apiClient from './apiClient.js'

class DashboardService {
  getMetrics() {
    return apiClient.get('/api/v1/dashboard/metrics')
  }
}

export default new DashboardService()
