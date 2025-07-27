// @ts-check
import apiClient from './apiClient.js';

class DashboardService {
  /**
   * Fetch dashboard metrics
   * @returns {Promise<import('axios').AxiosResponse<any>>}
   */
  getMetrics() {
    return apiClient.get('/api/v1/dashboard/metrics');
  }
}

export default new DashboardService();
