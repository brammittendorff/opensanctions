import click
import logging
from followthemoney.cli.util import write_object

from opensanctions.core import Dataset, Context, Entity, setup
from opensanctions.core.export import export_global_index
from opensanctions.core.http import cleanup_cache
from opensanctions.model.base import migrate_db


@click.group(help="OpenSanctions ETL toolkit")
@click.option("-v", "--verbose", is_flag=True, default=False)
@click.option("-q", "--quiet", is_flag=True, default=False)
def cli(verbose=False, quiet=False):
    level = logging.INFO
    if quiet:
        level = logging.WARNING
    if verbose:
        level = logging.DEBUG
    setup(log_level=level)


@cli.command("dump", help="Export the entities from a dataset")
@click.argument("dataset", default=Dataset.ALL, type=click.Choice(Dataset.names()))
@click.option("-o", "--outfile", type=click.File("w"), default="-")
def dump_dataset(dataset, outfile):
    dataset = Dataset.get(dataset)
    for entity in Entity.query(dataset):
        write_object(outfile, entity)


@cli.command("crawl", help="Crawl entities into the given dataset")
@click.argument("dataset", default=Dataset.ALL, type=click.Choice(Dataset.names()))
def crawl(dataset):
    dataset = Dataset.get(dataset)
    for source in dataset.sources:
        Context(source).crawl()


@cli.command("export", help="Export entities from the given dataset")
@click.argument("dataset", default=Dataset.ALL, type=click.Choice(Dataset.names()))
def export(dataset):
    dataset = Dataset.get(dataset)
    for dataset_ in dataset.datasets:
        context = Context(dataset_)
        context.export()
    export_global_index()


@cli.command("run", help="Run the full process for the given dataset")
@click.argument("dataset", default=Dataset.ALL, type=click.Choice(Dataset.names()))
def run(dataset):
    dataset = Dataset.get(dataset)
    for source in dataset.sources:
        Context(source).crawl()
    for dataset_ in dataset.datasets:
        context = Context(dataset_)
        context.export()
    export_global_index()


@cli.command("cleanup", help="Clean up caches")
def cleanup():
    cleanup_cache()


@cli.command("migrate", help="Create a new database autogenerated migration")
@click.option("-m", "--message", "message")
def migrate(message):
    migrate_db(message)