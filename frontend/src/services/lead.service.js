// @ts-check
import apiClient from './apiClient.js';
/** @typedef {import('../types.js').LeadData} LeadData */

class LeadService {
  /**
   * Send lead data to backend
   * @param {LeadData} leadData
   * @returns {Promise<import('axios').AxiosResponse>}
   */
  create(leadData) {
    return apiClient.post('/api/v1/leads/', leadData);
  }
}

export default new LeadService();
