var apiNoteAll = function(callback) {
    var method = 'GET'
    var path = '/api/note/all'
    ajax(method, path, '', callback)
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
        </div>
    `
    return t
}

var insertNote = function(note) {
    var noteCell = noteTemplate(note)
    var noteList = e('#id-todo-list')
    noteList.insertAdjacentHTML('beforeend', noteCell)
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
    loadNotes()
}

__main()
