/**
 * @typedef {Object} Option
 * @property {number} id
 * @property {string} text
 * @property {number} price_impact
 * @property {number} order
 */

/**
 * @typedef {Object} Question
 * @property {number} id
 * @property {string} text
 * @property {string} [description]
 * @property {'single-choice'|'slider'} question_type
 * @property {number} order
 * @property {Option[]} options
 */

/**
 * @typedef {Object} Quiz
 * @property {number} id
 * @property {string} title
 * @property {string} [description]
 * @property {Question[]} questions
 */

/**
 * @typedef {Object} LeadData
 * @property {string} email
 * @property {number} final_price
 * @property {Record<string, any>} answers_data
 */

export {};
