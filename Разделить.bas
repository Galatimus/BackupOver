Attribute VB_Name = "Module1"
Sub DivFile()
    Dim i As Long, s As String, ws As Worksheet	
    Application.ScreenUpdating = False: Set ws = ActiveSheet
	et = 184000
    For i = 1 To ws.UsedRange.Row + ws.UsedRange.Rows.Count - 1 Step et
        Workbooks.Add xlWBATWorksheet: ws.Rows(i & ":" & i + et).Copy [A1]
        s = Replace(ThisWorkbook.FullName, ".xls", "-" & (Fix(i / et) + 1) & ".xls")
        ActiveWorkbook.SaveAs s: ActiveWorkbook.Close
    Next
End Sub
