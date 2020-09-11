package strava

import (
	"net/http"
	"net/url"
	"time"
)

const (
	BaseURL string = "https://www.strava.com/"
)

type Client struct {
	CallbackURL  *url.URL
	baseURL      *url.URL
	clientID     string
	clientSecret string
	httpClient   *http.Client
}

func NewClient(httpClient *http.Client, callbackURL *url.URL, clientID, clientSecret string) (*Client, error) {
	u, _ := url.Parse(BaseURL)

	if callbackURL == nil {
		return nil, InvalidCallbackURLErr
	}

	if httpClient == nil {
		httpClient = http.DefaultClient
		httpClient.Timeout = time.Second * 10
	}

	if clientID == "" {
		return nil, InvalidClientIDErr
	}

	if clientSecret == "" {
		return nil, InvalidClientSecretErr
	}

	c := &Client{
		CallbackURL:  callbackURL,
		baseURL:      u,
		clientID:     clientID,
		clientSecret: clientSecret,
		httpClient:   httpClient,
	}

	return c, nil
}
