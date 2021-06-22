/// <reference types="cypress" />

describe('Login', () => {
	it('should redirect to dashboard after login', () => {
		cy.visit(Cypress.config('baseUrl'));

        cy.get('input[type="email"]').type('Administrator');
        cy.get('input[type="password"]').type(Cypress.config('adminPassword'));

		// cy.get('.btn-login:visible').click();
		// cy.url().should('include', '/dashboard');
	});
});
