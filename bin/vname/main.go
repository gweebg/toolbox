package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"os/exec"
	"regexp"
	"strings"
)

const (
	VagrantPath = "vagrant"
	StopColumn  = "provider"
)

type GlobalStatusEntry struct {
	Id   string
	Name string
}

func NewGlobalStatusEntry(line string, stop int) GlobalStatusEntry {

	line = line[:stop]

	pattern := `^(\w+)\s+([\w\s]*)$`
	re := regexp.MustCompile(pattern)

	matches := re.FindStringSubmatch(line)
	if len(matches) <= 0 {
		log.Fatalf("no matches in '%v' for pattern '%v'", line, pattern)
	}

	return GlobalStatusEntry{
		Id:   strings.TrimSpace(matches[1]),
		Name: strings.TrimSpace(matches[2]),
	}
}

func ParseGlobalStatus(output string, lookup string) (GlobalStatusEntry, error) {

	index := 0
	stop := -1

	scanner := bufio.NewScanner(strings.NewReader(output))
	for scanner.Scan() {
		line := scanner.Text()

		if strings.TrimSpace(line) == "" {
			break
		}

		if index == 0 {
			stop = strings.Index(line, StopColumn)
			if stop == -1 {
				return GlobalStatusEntry{}, fmt.Errorf("can't find column '%v' in header of output of '%v global-status'", StopColumn, VagrantPath)
			}
		}

		if index > 1 {
			entry := NewGlobalStatusEntry(line, stop)
			if entry.Name == lookup {
				return entry, nil
			}
		}
		index++
	}

	if err := scanner.Err(); err != nil {
		return GlobalStatusEntry{}, fmt.Errorf("scanner error: %v", err)
	}

	return GlobalStatusEntry{}, fmt.Errorf("name '%v' does not match any box name", lookup)
}

func CheckVagrant() bool {
	_, err := exec.LookPath(VagrantPath)
	return err == nil
}

func GetGlobalStatusOutput() (string, error) {
	cmd := exec.Command(VagrantPath, "global-status")
	stdout, err := cmd.Output()
	return string(stdout), err
}

func GetGlobalStatusEntry(name string) (GlobalStatusEntry, error) {

	out, err := GetGlobalStatusOutput()
	if err != nil {
		return GlobalStatusEntry{}, err
	}

	entry, err := ParseGlobalStatus(out, name)
	if err != nil {
		return GlobalStatusEntry{}, err
	}

	return entry, nil
}

func main() {

	exists := CheckVagrant()
	if !exists {
		log.Fatalf("cannot find '%v' installed on this system", VagrantPath)
	}

	entry, err := GetGlobalStatusEntry(os.Args[1])
	if err != nil {
		log.Fatal(err)
	}

	fmt.Print(entry.Id)
}
