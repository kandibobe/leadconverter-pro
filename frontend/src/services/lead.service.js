import apiClient from './apiClient.js';

class LeadService {
  create(leadData) {
    return apiClient.post('/api/v1/leads/submit', leadData);
  }
}

export default new LeadService();