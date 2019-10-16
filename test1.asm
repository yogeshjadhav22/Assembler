section .data
	num1 dd 10,20,30,40,50
	gaur db 'this is string'
	num2 dd  100,20
	msg1 db 'my name is yogesh'
	num3 dd 10,20,30,40
section .bss	
	n1 resd 11
	n2 resd 12
section .text
	global main
main:   xor eax,eax
	xor ebx,ebx
	push n1
	push num1
	add esp,8
	push n2
	push num2    
	add esp,8
	mov eax,ebx
	mov eax,10
	mov ecx,edx
	mov esi,edi
	mov eax,dword[n1]
	mov ecx,dword[n2]
	mov edx,eax
	div ecx
	call printf
	pusha
	push eax
	push msg1
	add esp,8
	popa
	push edx
	push msg1
	add esp,8
	ret
