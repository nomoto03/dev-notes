package main

imoiport "fmt"

func main()  {
	var (
		u8 uint8 = 255
		i8 int8 = 127
		f32 float32 = 0.2
		c64 complex64 = -5 + 12i
	)
	fmt.Println(u8, i8, f32, c64)
	fmt.Printf("type=%T value=%v\n", u8, u8)
}