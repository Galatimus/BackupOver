Sub RemoveFolderWithContent()
    Dim sFolder As String
   	sFolder = "C:\Users\Oleg\Desktop\zem"
	sFolder = sFolder & IIf(Right(sFolder, 1) = Application.PathSeparator, "", Application.PathSeparator)
	Shell "cmd /c rd /S/Q """ & sFolder & """"
End Sub