import apiClient from './apiClient.js';

class LeadService {
  create(leadData) {
    return apiClient.post('/api/v1/leads/', leadData);
  }
}

export default new LeadService();
