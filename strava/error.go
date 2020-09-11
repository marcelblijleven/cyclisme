package strava

import "errors"

var InvalidClientIDErr = errors.New("invalid client id received")
var InvalidClientSecretErr = errors.New("invalid client secret received")
var InvalidCallbackURLErr = errors.New("invalid callback url provided")
