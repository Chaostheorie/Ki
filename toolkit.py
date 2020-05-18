#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import click
import os
import ujson
import logging
import shutil


@click.group()
@click.option('--debug/--no-debug', default=False,
              help="Enables or disables debug")
@click.pass_context
def cli(ctx, debug):
    """
    Ki cli toolkit
    """
    # Configure logging
    ctx.debug = debug
    levels = {True: logging.DEBUG, False: logging.INFO}
    logging.basicConfig(level=levels[debug])
    ctx.obj = logging.getLogger("Ki Toolkit")
    return


@cli.command("download")
@click.option("--reform", is_flag=True,
              help="Reform downloaded content after download")
@click.option("--purify", is_flag=True,
              help="Reform downloaded content after download")
@click.option("--output", type=click.Path(exists=False),
              default="strassenbaeume.xml",
              help="Output file (XML)")
@click.pass_context
def _download(ctx, purify, reform, output):
    """Downloads the dataset with wfs-downloader"""
    ctx.obj.info("Executing 'wfs-downloader assets/config.yaml'")

    if output != "strassenbaeume.xml":  # Check if default
        conf = "assets/tmp_config.yaml"
        if os.path.isfile(output):
            ctx.obj.info(f"{output} will be overwritten")
        with open("assets/config.yaml", "r") as f:
            bak = f.read().replace("strassenbaeume.xml", output)
        with open("assets/tmp_config.yaml", "w+") as f:
            f.write(bak)
    else:
        conf = "assets/config.yaml"
    if not os.path.exists("/tmp/wfs-downloader"):
        ctx.obj.info("Creating /tmp/wfs-downloader as tmp folder")
        os.mkdir("/tmp/wfs-downloader")
    os.system(f"wfs-downloader {conf}")
    ctx.obj.info("Removing tmp folder")
    shutil.rmtree("/tmp/wfs-downloader")
    if output != "strassenbaueme.xml":
        os.remove(conf)
    if reform is True:
        tmp = output.replace(".xml", ".json")
        ctx.obj.info(f"Invoking reform --input {output} --ouput {tmp} ")
        ctx.invoke(_reform, input=output,
                   output=tmp)
    if purify is True:
        tmp = output.replace(".xml", ".json")
        ctx.obj.info(f"Invoking purify --input {tmp} --ouput {tmp} ")
        ctx.invoke(_purify, input=tmp,
                   output=tmp)


@cli.command("reform")
@click.option("--input", type=click.Path(exists=True),
              default="strassenbaeume.xml",
              help="Input File (XML)")
@click.option("--output", type=click.Path(exists=True),
              default="output.json",
              help="Output file (JSON)")
@click.pass_context
def _reform(ctx, input, output):
    """Reforms dataset to json"""
    import xmltodict
    from pyproj import Transformer
    from ki.tools import reform as proccess

    transformer = Transformer.from_crs("EPSG:25833", "EPSG:4326")
    ctx.obj.info("Coordinate transformer initialized")

    ctx.obj.info(f"Start file parsing from {input} ...")
    with open(input, "rb") as f:
        data = xmltodict.parse(f)
        data = data["wfs:FeatureCollection"]
        ctx.obj.info("Finished parsing. Start reforming ...")
        trees = [proccess(transformer, data["wfs:member"][i]["fis:s_wfs_baumbestand"])
                 for i in range(int(data["@numberReturned"]))]
    ctx.obj.info("Reforming finished")

    ctx.obj.info(f"Writing data to {output} ...")
    with open(output, "w+") as f:
        ujson.dump(trees, f, indent=4)
    ctx.obj.info("Writing data finished.")


@cli.command("parse")
@click.option("--input", type=click.Path(exists=True),
              default="output.json",
              help="Input file (JSON) (default: output.json)")
@click.pass_context
def _parser(ctx, input):
    """Ingests data from json file into database (ki.config is used)"""
    from ki import db
    from ki.models import Trees

    ctx.obj.info(f"Start loading {input}")
    with open(input) as f:
        data = ujson.load(f)
        ctx.obj.info("Finished loading. Start ingesting data ...")
        [db.session.add(Trees.parse(data[i])) for i in range(len(data))]
    ctx.obj.info("Finished adding data. Commiting to database ...")
    db.session.commit()
    ctx.obj.info("Finished Comitting.")


@cli.command("purify")
@click.option("--input", type=click.Path(exists=True),
              default="output.json",
              help="Input file (JSON) (default: output.json)")
@click.option("--output", type=click.Path(exists=False),
              default="output.json",
              help="Output file (JSON) (default: output.json)")
@click.option("--dry-run", is_flag=True,
              help="Dry run without (over)writting output")
@click.pass_context
def _purify(ctx, input, output, dry_run):
    """
    Removes duplicate trees from reformed dataset
    (due to reforming accuracy is lost and some trees are on the same position)
    """
    ctx.obj.info(f"Start loding {input}")
    with open(input) as f:
        try:
            data = ujson.load(f)
        except ValueError:
            raise ValueError(f"Source file {input} was not loadable")
    ctx.obj.info("Finished loading data. Start purifying")
    ctx.obj.warning("Purifying cost a huge amount of time (incremental)")

    unique = []
    i = 0
    length = len(data)
    _length = length
    while i+1 != length:
        if data[i]["coords"] not in unique:
            unique.append(data[i]["coords"])
            i += 1
        else:
            data.pop(i)
            length -= 1
        print("\r {}% Progress \r".format(format(i/_length*100, ".2f")),
              end="")

    ctx.obj.info(f"Finished purifying. Reduced data by {_length-length} items.")

    if dry_run:
        ctx.obj.info("Not writting data (dry run)...")
        return
    elif input == output:
        ctx.obj.info("Start overwritting data ...")
    else:
        ctx.obj.info(f"Start writting data to {output} ...")

    with open(output, "w+") as f:
        ujson.dump(data, f)


if __name__ == "__main__":
    cli()
