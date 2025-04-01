use serde::Deserialize;
use std::env;
use dotenv::dotenv;

#[derive(Deserialize)]
pub struct Config {
    pub server_addr: String,
    pub database_url: String,
    pub nats_url: String,
    pub jwt_secret: String,
}

impl Config {
    pub fn from_env() -> Result<Self, config::ConfigError> {
        dotenv().ok();
        let mut cfg = config::Config::default();
        cfg.merge(config::Environment::default())?;
        cfg.try_into()
    }
}
