// @ts-check
import apiClient from './apiClient.js';
/** @typedef {import('../types.js').LeadData} LeadData */

class AdminLeadService {
  /**
   * Get leads list
   * @returns {Promise<import('axios').AxiosResponse<LeadData[]>>}
   */
  getLeads() {
    return apiClient.get('/api/v1/leads/');
  }
}

export default new AdminLeadService();
