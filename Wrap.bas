Sub Wraptext()
Dim ws As Worksheet
For Each ws In Worksheets
    ws.Cells.WrapText = false
Next ws
End Sub