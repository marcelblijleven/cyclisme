package strava

import (
	"net/http"
	"net/url"
	"testing"
)

var callbackURL, _ = url.Parse("http://test.nu")

func TestNewClient(t *testing.T) {
	httpClient := &http.Client{}
	c, err := NewClient(httpClient, callbackURL, "c0ffee", "tops3cr3t")

	if err != nil {
		t.Errorf("expected err to be non nil")
	}

	if c == nil {
		t.Errorf("did not setup client correctly")
	}

	if c.httpClient != httpClient {
		t.Errorf("did not set provided http client as client")
	}

	if c.CallbackURL != callbackURL {
		t.Errorf("did not set up callback url correctly")
	}

	if c.clientID != "c0ffee" {
		t.Errorf("did not set up client id correctly")
	}

	if c.clientSecret != "tops3cr3t" {
		t.Errorf("did not set up client secret correctly")
	}
}

func TestNewClient_invalidCallbackURL(t *testing.T) {
	c, err := NewClient(nil, nil, "c0ffee", "tops3cr3t")

	if err != InvalidCallbackURLErr {
		t.Errorf("expected err to equal %v instead got %v", InvalidCallbackURLErr.Error(), err.Error())
	}

	if c != nil {
		t.Errorf("expected client to be nil")
	}
}

func TestNewClient_useDefaultHTTPClient(t *testing.T) {
	c, err := NewClient(nil, callbackURL, "c0ffee", "tops3cr3t")

	if err != nil {
		t.Errorf("expected err to be non nil")
	}

	if c.httpClient == nil {
		t.Errorf("did not setup client correctly")
	}

	if c.httpClient != http.DefaultClient {
		t.Errorf("expected client to equal default client")
	}
}

func TestNewClient_invalidClientIDReturnsInvalidClientIDErr(t *testing.T) {
	_, err := NewClient(nil, callbackURL, "", "tops3cr3t")

	if err == nil {
		t.Errorf("expected err to be non nil")
	}

	if err != InvalidClientIDErr {
		t.Errorf("expected err to equal %v instead got %v", InvalidClientIDErr.Error(), err.Error())
	}
}

func TestNewClient_invalidClientSecretReturnsInvalidClientSecretErr(t *testing.T) {
	_, err := NewClient(nil, callbackURL, "c0ffee", "")

	if err == nil {
		t.Errorf("expected err to be non nil")
	}

	if err != InvalidClientSecretErr {
		t.Errorf("expected err to equal %v instead got %v", InvalidClientSecretErr.Error(), err.Error())
	}
}
