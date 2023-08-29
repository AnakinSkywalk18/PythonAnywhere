/* ALL CODE BELOW DOES NOT WORK*/
/* 

HTML CODE:
<button type="button" class="close" onClick="deleteNote({{ note.id }}"

note.id is a parameter
deleteNote is a function written in this index.js file

*/

/*
function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

/delete-note should be an end-point/app route that must be created in views.py
the /telete-note should have a POST method associated with it in views.py

this is how the code should be for it in views.py:

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

What does that function do?

note takes in data from POST request and loads that data as a json object
uses noteId to access the note with that id
if the note exists,
    if the current user IS THE user associated with the note,
        DELETE the note
        Return an empty note
*/

function console_log() {
    console.log("hi")
}
