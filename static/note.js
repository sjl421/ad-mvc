var apiNoteAll = function(callback) {
    var method = 'GET'
    var path = '/api/note/all'
    ajax(method, path, '', callback)
}

var apiNoteAdd = function(data, callback) {
    var method = 'POST'
    var token = csrfToken()
    var path = `/api/note/add?csrf_token=${token}`
    ajax(method, path, data, callback)
}

var apiNoteDelete = function(data, callback) {
    var method = 'POST'
    var token = csrfToken()
    var path = `/api/note/delete?csrf_token=${token}`
    ajax(method, path, data, callback)
}

var apiNoteUpdate = function(data, callback) {
    var method = 'POST'
    var token = csrfToken()
    var path = `/api/note/update?csrf_token=${token}`
    ajax(method, path, data, callback)
}

var csrfToken = function() {
    var token = e('#id-csrf-token').innerText
    return token
}

var noteTemplate = function(note) {
    // Note DOM
    var t = `
        <div class="note-cell" data-id="${note.id}">
            <h3 class="note-title">${escapedHTML(note.title)}</h3>
            <h4>
                <span>&lt</span>
                <span class="note-username">${escapedHTML(note.username)}</span>
                <span>&gt</span>
            </h4>
            <div class="note-content">${escapedHTML(note.content)}</div>

            <button class="note-edit">编辑</button>
            <button class="note-delete">删除</button>

            <div class="note-update-form-container">
            </div>
        </div>
    `
    return t
}

var noteUpdateTemplate = function(title, content) {
    var t = `
        <div class="note-update-form">
            <input type="text" class="note-title-input" value="${title}">
            <input type="text" class="note-content-input" value="${content}">
            <button class="note-update">更新留言</button>
        </div>
    `
    return t
}

var insertNote = function(note) {
    var noteCell = noteTemplate(note)
    var noteList = e('#id-note-list')
    noteList.insertAdjacentHTML('beforeEnd', noteCell)
}

var insertNoteUpdateForm = function(noteCell) {
    var formContainer = noteCell.querySelector('.note-update-form-container')
    var titleField = noteCell.querySelector('.note-title')
    var contentField = noteCell.querySelector('.note-content')

    var title = titleField.innerText
    var content = contentField.innerText

    var t = noteUpdateTemplate(title, content)
    formContainer.innerHTML = t
}

var updateNote = function(noteCell, note) {
    var titleField = noteCell.querySelector('.note-title')
    var contentField = noteCell.querySelector('.note-content')

    titleField.innerText = note.title
    contentField.innerText = note.content
}

var bindNoteAddEvent = function() {
    var addForm = e('#id-note-add-form')
    var b = addForm.querySelector('.note-add')
    b.addEventListener('click', function() {
        var titleInput = addForm.querySelector('.note-title-input')
        var contentInput = addForm.querySelector('.note-content-input')

        var title = titleInput.value
        var content = contentInput.value
        var form = {
            title: title,
            content: content,
        }

        apiNoteAdd(form, function(response) {
            var note = response
            log('add note', note)
            insertNote(note)
        })
    })
}

var bindNoteDeleteEvent = function() {
    var noteList = e('#id-note-list')
    noteList.addEventListener('click', function(event) {
        var self = event.target
        if (self.classList.contains('note-delete')) {
            var noteCell = self.closest('.note-cell')
            var noteId = noteCell.dataset.id
            var form = {
                id: noteId,
            }

            apiNoteDelete(form, function(response) {
                log('delete note', response)
                noteCell.remove()
            })
        }
    })
}

var bindNoteEditEvent = function() {
    var noteList = e('#id-note-list')
    noteList.addEventListener('click', function(event) {
        var self = event.target
        if (self.classList.contains('note-edit')) {
            var noteCell = self.closest('.note-cell')
            insertNoteUpdateForm(noteCell)
        }
    })
}

var bindNoteUpdateEvent = function() {
    var noteList = e('#id-note-list')
    noteList.addEventListener('click', function(event) {
        var self = event.target
        if (self.classList.contains('note-update')) {
            var noteCell = self.closest('.note-cell')
            var updateForm = noteCell.querySelector('.note-update-form')
            var titleInput = noteCell.querySelector('.note-title-input')
            var contentInput = noteCell.querySelector('.note-content-input')

            var noteId = noteCell.dataset.id
            var title = titleInput.value
            var content = contentInput.value
            var form = {
                id: noteId,
                title: title,
                content: content,
            }

            apiNoteUpdate(form, function(response) {
                var note = response
                log('update note', note)

                updateNote(noteCell, note)
                updateForm.remove()
            })
        }
    })
}

var bindEvents = function () {
    bindNoteAddEvent()
    bindNoteDeleteEvent()
    bindNoteEditEvent()
    bindNoteUpdateEvent()
}

var loadNotes = function() {
    apiNoteAll(function(response) {
        var notes = response
        log('load all', notes)

        for(var i = 0; i < notes.length; i++) {
            var note = notes[i]
            insertNote(note)
        }
    })
}

var __main = function() {
    bindEvents()
    loadNotes()
}

__main()
