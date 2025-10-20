import reflex as rx

config = rx.Config(
    app_name="prueba_reflex",
    env=rx.Env.DEV,
    db_url="sqlite:///reflex.db",
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
)
