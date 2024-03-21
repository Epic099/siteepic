const roomselect = document.getElementById("roomselect")
function selectRoom()
{
    var room_name = roomselect.options[roomselect.selectedIndex].text;
    if(room_name != "" && room_name != null)
    {
        window.location.href = "/chess/" + room_name
    }
}