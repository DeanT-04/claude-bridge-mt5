"""Command-line entry point: `uv run propquant --help`."""

import typer
from rich.console import Console

from propquant import paths
from propquant.vault.skeleton import init_vault
from propquant.vault.sync import mirror

app = typer.Typer(no_args_is_help=True, help="Prop Quant Lab research pipeline.")
vault_app = typer.Typer(no_args_is_help=True, help="Obsidian knowledge base.")
app.add_typer(vault_app, name="vault")
console = Console()


@vault_app.command("init")
def vault_init() -> None:
    """Create the vault folders, Home dashboard and note templates (never overwrites)."""
    root = paths.vault_dir()
    created = init_vault(root)
    console.print(f"Vault: {root}  ({len(created)} files created)")


@vault_app.command("sync")
def vault_sync() -> None:
    """Mirror the vault into docs/vault for the git backup."""
    res = mirror(paths.vault_dir(), paths.DOCS_VAULT_DIR)
    console.print(
        f"copied {len(res.copied)}, deleted {len(res.deleted)}, unchanged {res.unchanged}"
    )
