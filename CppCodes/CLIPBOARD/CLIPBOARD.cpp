#include<iostream>
#include<windows.h>


int main(int argc, char** argv)
{
	HWND hWnd = NULL;
	OpenClipboard(hWnd);
	EmptyClipboard();
	HANDLE hHandle = GlobalAlloc(GMEM_FIXED, 1000);
	char *pData = (char*)GlobalLock(hHandle);
	strcpy_s(pData, 1000, argv[1]);
	SetClipboardData(CF_TEXT, hHandle);
	GlobalUnlock(hHandle);
	CloseClipboard();
}