#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ki import ki
from config import development


if __name__ == "__main__":
    ki.config.from_object(development)
    ki.run()
