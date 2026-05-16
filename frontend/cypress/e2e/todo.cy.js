describe('R8 - Todo item GUI tests', () => {
  let uid
  let name
  let email
  let taskTitle

  const videoKey = 'dQw4w9WgXcQ'

  function login() {
    cy.visit('http://localhost:3000')

    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)

    cy.get('form')
      .submit()

    cy.get('h1')
      .should('contain.text', 'Your tasks, ' + name)
  }

  function createTaskAndOpenIt() {
    cy.get('#title')
      .type(taskTitle)

    cy.get('#url')
      .type(videoKey)

    cy.get('input[type=submit][value="Create new Task"]')
      .click()

    // The title overlay exists, but it is hidden with CSS opacity until hover.
    // Therefore we check that it exists and force-click it.
    cy.contains('.title-overlay', taskTitle, { timeout: 10000 })
      .should('exist')
      .click({ force: true })

    cy.get('.todo-list', { timeout: 10000 })
      .should('be.visible')
  }

  beforeEach(function () {
    const stamp = Date.now()

    email = `todo.test.${stamp}@example.com`
    name = 'Todo Tester'
    taskTitle = `Todo task ${stamp}`

    const user = {
      email: email,
      firstName: 'Todo',
      lastName: 'Tester'
    }

    cy.request({
      method: 'POST',
      url: 'http://localhost:5000/users/create',
      form: true,
      body: user
    }).then((response) => {
      uid = response.body._id.$oid
    })

    login()
    createTaskAndOpenIt()
  })

  it('R8UC1 - creates a new todo item for a task', () => {
    const todoText = 'Read the article'

    cy.get('input[placeholder="Add a new todo item"]')
      .type(todoText)

    cy.get('form.inline-form')
      .submit()

    cy.contains('.todo-item', todoText, { timeout: 10000 })
      .should('be.visible')
  })

  it('R8UC2 - toggles a todo item as done', () => {
    cy.contains('.todo-item', 'Watch video', { timeout: 10000 })
      .within(() => {
        cy.get('.checker')
          .click()
      })

    cy.contains('.todo-item', 'Watch video')
      .find('.checker')
      .should('have.class', 'checked')
  })

  it('R8UC3 - deletes a todo item from a task', () => {
    const todoText = 'Todo item to delete'

    // First create a unique todo item so the delete test does not depend on the default item.
    cy.get('input[placeholder="Add a new todo item"]')
      .type(todoText)

    cy.get('form.inline-form')
      .submit()

    cy.contains('.todo-item', todoText, { timeout: 10000 })
      .should('be.visible')

    // Then delete the todo item.
    cy.contains('.todo-item', todoText)
      .within(() => {
        cy.get('.remover')
          .click()
      })

    // The todo item should no longer be visible in the GUI.
    cy.contains('.todo-item', todoText)
      .should('not.exist')
  })

  afterEach(function () {
    if (uid) {
      cy.request({
        method: 'DELETE',
        url: `http://localhost:5000/users/${uid}`,
        failOnStatusCode: false
      })
    }
  })
})